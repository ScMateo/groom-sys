from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get("", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """
    Endpoint de diagnóstico para verificar que la API esté activa
    y la conexión con PostgreSQL en Supabase funcione correctamente.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "DATABASE_ERROR",
                "message": f"Error de conexión con la base de datos: {str(e)}"
            }
        )