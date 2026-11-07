import asyncio
import logging
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, init_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.farmer_profile import FarmerProfile
from app.models.knowledge import KnowledgeArticle
from app.models.notification import Notification
from app.seeds.knowledge_seed import KNOWLEDGE_ARTICLES_SEED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")


async def seed_database():
    logger.info("Initializing database schema...")
    await init_db()

    async with AsyncSessionLocal() as db:
        # 1. Seed Demo User
        user_stmt = select(User).where(User.phone == "9876543210")
        res = await db.execute(user_stmt)
        demo_user = res.scalar_one_or_none()

        if not demo_user:
            logger.info("Creating demo farmer user (phone: 9876543210)...")
            demo_user = User(
                full_name="Ramesh Patil",
                phone="9876543210",
                email="ramesh.patil@agrivision.ai",
                hashed_password=get_password_hash("Password123!"),
                preferred_language="mr",
                preferred_theme="light",
                is_active=True,
            )
            db.add(demo_user)
            await db.flush()

            profile = FarmerProfile(
                user_id=demo_user.id,
                village="Baramati",
                district="Pune",
                state="Maharashtra",
                farm_area_hectares=2.5,
                primary_crops=["Tomato", "Sugarcane", "Wheat"],
                soil_type="Black Soil",
                irrigation_type="Drip Irrigation",
            )
            db.add(profile)
            await db.flush()

            # Add welcome notification
            notif = Notification(
                user_id=demo_user.id,
                title="Agrivision AI+ मध्ये आपले स्वागत आहे!",
                message="तुमच्या शेतातील पिकांची आरोग्य तपासणी करण्यासाठी पानाचा फोटो अपलोड करा.",
                type="info",
                is_read=False,
            )
            db.add(notif)
            await db.flush()
            logger.info("Demo farmer created.")

        # 2. Seed Knowledge Articles
        logger.info("Seeding knowledge base articles...")
        articles_added = 0
        for item in KNOWLEDGE_ARTICLES_SEED:
            art_stmt = select(KnowledgeArticle).where(KnowledgeArticle.title_en == item["title_en"])
            art_res = await db.execute(art_stmt)
            existing = art_res.scalar_one_or_none()

            if not existing:
                article = KnowledgeArticle(
                    category=item["category"],
                    title_en=item["title_en"],
                    title_mr=item["title_mr"],
                    title_hi=item["title_hi"],
                    content_en=item["content_en"],
                    content_mr=item["content_mr"],
                    content_hi=item["content_hi"],
                    tags=item["tags"],
                    is_published=item.get("is_published", True),
                )
                db.add(article)
                articles_added += 1

        await db.commit()
        logger.info(f"Database seeding completed successfully. Added {articles_added} articles.")


if __name__ == "__main__":
    asyncio.run(seed_database())
