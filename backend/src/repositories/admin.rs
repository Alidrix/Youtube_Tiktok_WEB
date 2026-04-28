use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct AdminOverview {
    pub users: i64,
    pub subscriptions: i64,
    pub message: &'static str,
}
