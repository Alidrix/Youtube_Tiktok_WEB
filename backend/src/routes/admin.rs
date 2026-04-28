use axum::{extract::State, Json};
use serde_json::json;

use crate::{error::AppError, services::access::ensure_admin, state::AppState, AuthBearer};

pub async fn overview(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<serde_json::Value>, AppError> {
    ensure_admin(&state.pool, &auth.sub).await?;
    let users: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM users")
        .fetch_one(&state.pool)
        .await?;
    let subscriptions: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM subscriptions")
        .fetch_one(&state.pool)
        .await?;
    Ok(Json(
        json!({"users": users, "subscriptions": subscriptions, "sources": "à connecter", "jobs": "à connecter", "system": "à connecter"}),
    ))
}

pub async fn users(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<serde_json::Value>, AppError> {
    ensure_admin(&state.pool, &auth.sub).await?;
    Ok(Json(json!({"message": "admin users endpoint ready"})))
}
pub async fn sources(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<serde_json::Value>, AppError> {
    ensure_admin(&state.pool, &auth.sub).await?;
    Ok(Json(json!({"message": "admin sources endpoint ready"})))
}
pub async fn jobs(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<serde_json::Value>, AppError> {
    ensure_admin(&state.pool, &auth.sub).await?;
    Ok(Json(json!({"message": "admin jobs endpoint ready"})))
}
pub async fn system(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<serde_json::Value>, AppError> {
    ensure_admin(&state.pool, &auth.sub).await?;
    Ok(Json(json!({"message": "admin system endpoint ready"})))
}
