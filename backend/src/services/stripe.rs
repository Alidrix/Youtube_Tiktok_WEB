use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct BillingMessage {
    pub enabled: bool,
    pub message: &'static str,
    pub checkout_url: Option<String>,
    pub url: Option<String>,
}

pub fn billing_enabled() -> bool {
    std::env::var("STRIPE_SECRET_KEY")
        .ok()
        .filter(|v| !v.is_empty())
        .is_some()
        && std::env::var("STRIPE_PRICE_PRO")
            .ok()
            .filter(|v| !v.is_empty())
            .is_some()
        && std::env::var("STRIPE_PRICE_STUDIO")
            .ok()
            .filter(|v| !v.is_empty())
            .is_some()
}

pub fn not_configured() -> BillingMessage {
    BillingMessage {
        enabled: false,
        message: "billing is not configured yet",
        checkout_url: None,
        url: None,
    }
}
