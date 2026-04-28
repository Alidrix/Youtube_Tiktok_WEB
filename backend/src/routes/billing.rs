use axum::Json;
use serde::{Deserialize, Serialize};

use crate::services::stripe::{billing_enabled, not_configured, BillingMessage};

#[derive(Debug, Serialize)]
pub struct BillingStatus {
    pub provider: &'static str,
    pub enabled: bool,
    pub message: &'static str,
}

#[derive(Debug, Deserialize)]
pub struct CheckoutPayload {
    pub plan: String,
}

pub async fn billing_status() -> Json<BillingStatus> {
    let enabled = billing_enabled();
    Json(BillingStatus {
        provider: "stripe",
        enabled,
        message: if enabled {
            "billing configured"
        } else {
            "billing is not configured yet"
        },
    })
}

pub async fn billing_checkout(Json(payload): Json<CheckoutPayload>) -> Json<BillingMessage> {
    if !billing_enabled() {
        return Json(not_configured());
    }

    Json(BillingMessage {
        enabled: true,
        message: "checkout ready",
        checkout_url: Some(format!("/checkout/{}", payload.plan)),
        url: None,
    })
}

pub async fn billing_portal() -> Json<BillingMessage> {
    if !billing_enabled() {
        return Json(not_configured());
    }

    Json(BillingMessage {
        enabled: true,
        message: "portal ready",
        checkout_url: None,
        url: Some("/subscription".into()),
    })
}

pub async fn billing_webhook() -> Json<BillingMessage> {
    Json(not_configured())
}
