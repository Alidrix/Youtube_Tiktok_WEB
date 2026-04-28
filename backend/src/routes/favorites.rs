use axum::{
    extract::{Path, State},
    Json,
};
use serde::Deserialize;

use crate::{
    error::{ApiMessage, AppError},
    repositories::favorites,
    state::AppState,
    AuthBearer,
};

#[derive(Debug, Deserialize)]
pub struct FavoritePayload {
    pub platform: String,
    pub trend_id: String,
}

async fn user_id_from_username(state: &AppState, username: &str) -> Result<uuid::Uuid, AppError> {
    sqlx::query_scalar("SELECT id FROM users WHERE username = $1")
        .bind(username)
        .fetch_one(&state.pool)
        .await
        .map_err(AppError::from)
}

pub async fn list_favorites(
    auth: AuthBearer,
    State(state): State<AppState>,
) -> Result<Json<Vec<favorites::FavoriteItem>>, AppError> {
    let user_id = user_id_from_username(&state, &auth.sub).await?;
    Ok(Json(favorites::list(&state.pool, user_id).await?))
}

pub async fn add_favorite(
    auth: AuthBearer,
    State(state): State<AppState>,
    Json(payload): Json<FavoritePayload>,
) -> Result<Json<ApiMessage>, AppError> {
    let user_id = user_id_from_username(&state, &auth.sub).await?;
    favorites::create(&state.pool, user_id, &payload.platform, &payload.trend_id).await?;
    Ok(Json(ApiMessage {
        message: "favorite saved".into(),
    }))
}

pub async fn delete_favorite(
    auth: AuthBearer,
    State(state): State<AppState>,
    Path((platform, trend_id)): Path<(String, String)>,
) -> Result<Json<ApiMessage>, AppError> {
    let user_id = user_id_from_username(&state, &auth.sub).await?;
    favorites::delete(&state.pool, user_id, &platform, &trend_id).await?;
    Ok(Json(ApiMessage {
        message: "favorite removed".into(),
    }))
}
