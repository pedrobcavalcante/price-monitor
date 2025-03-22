from fastapi import APIRouter
from src.application.services.scraping_service import ScrapingService
from src.application.services.notification_service import NotificationService

router = APIRouter()

scraping_service = ScrapingService()
notification_service = NotificationService()

@router.get("/products")
async def get_products():
    products = scraping_service.get_all_products()
    return products

@router.get("/notifications")
async def get_notifications():
    notifications = notification_service.get_all_notifications()
    return notifications

@router.post("/notifications")
async def create_notification(notification_data: dict):
    notification_service.create_notification(notification_data)
    return {"message": "Notification created successfully."}