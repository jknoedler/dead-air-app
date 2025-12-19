from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routers import auth, upload, activity, suggestions, oauth_router
from .database import init_db
from .services.sync_engine import SyncManager
from .jobs.refund_eligibility import check_refund_eligibility

app = FastAPI(title="Social Media Upload Service")
sync_manager = SyncManager()
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def on_startup():
    await init_db()
    # Start the sync engine in the background
    asyncio.create_task(sync_manager.start())
    # Schedule nightly refund eligibility check at midnight
    scheduler.add_job(check_refund_eligibility, "cron", hour=0, minute=0)
    scheduler.start()

# Session for OAuth state
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key"))

# CORS (allow frontend dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(oauth_router.router, prefix="/api/oauth", tags=["oauth"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(activity.router, prefix="/api/activity", tags=["activity"])
app.include_router(suggestions.router, prefix="/api/suggestions", tags=["suggestions"])
