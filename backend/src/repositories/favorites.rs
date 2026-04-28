use serde::Serialize;
use sqlx::PgPool;
use uuid::Uuid;

use crate::error::AppError;

#[derive(Debug, Serialize, sqlx::FromRow)]
pub struct FavoriteItem {
    pub platform: String,
    pub trend_id: String,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

pub async fn list(pool: &PgPool, user_id: Uuid) -> Result<Vec<FavoriteItem>, AppError> {
    let rows = sqlx::query_as::<_, FavoriteItem>(
        "SELECT platform, trend_id, created_at FROM favorites WHERE user_id = $1 ORDER BY created_at DESC",
    )
    .bind(user_id)
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn create(
    pool: &PgPool,
    user_id: Uuid,
    platform: &str,
    trend_id: &str,
) -> Result<(), AppError> {
    sqlx::query("INSERT INTO favorites (user_id, platform, trend_id) VALUES ($1, $2, $3) ON CONFLICT (user_id, platform, trend_id) DO NOTHING")
        .bind(user_id)
        .bind(platform)
        .bind(trend_id)
        .execute(pool)
        .await?;
    Ok(())
}

pub async fn delete(
    pool: &PgPool,
    user_id: Uuid,
    platform: &str,
    trend_id: &str,
) -> Result<(), AppError> {
    sqlx::query("DELETE FROM favorites WHERE user_id = $1 AND platform = $2 AND trend_id = $3")
        .bind(user_id)
        .bind(platform)
        .bind(trend_id)
        .execute(pool)
        .await?;
    Ok(())
}
