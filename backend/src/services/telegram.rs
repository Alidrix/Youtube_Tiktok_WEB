use crate::{config::TelegramConfig, error::AppError};

#[derive(Debug, Clone)]
pub struct TelegramAlertMessage {
    pub chat_id: String,
    pub title: String,
    pub platform: String,
    pub region: Option<String>,
    pub category: Option<String>,
    pub views_per_hour: Option<i64>,
    pub trend_score: Option<f64>,
    pub url: Option<String>,
}

pub async fn send_telegram_alert(
    config: &TelegramConfig,
    message: TelegramAlertMessage,
) -> Result<(), AppError> {
    if !config.is_configured() {
        tracing::warn!("Telegram is not configured; skipping Telegram alert delivery");
        return Ok(());
    }
    let text = format_telegram_message(&message);
    let endpoint = format!(
        "https://api.telegram.org/bot{}/sendMessage",
        config.bot_token
    );
    let payload = serde_json::json!({"chat_id": message.chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": false});
    let client = reqwest::Client::new();
    let response = client
        .post(endpoint)
        .json(&payload)
        .send()
        .await
        .map_err(|err| AppError::Config(format!("Telegram send failed: {}", err)))?;
    if !response.status().is_success() {
        let status = response.status();
        let body = response.text().await.unwrap_or_default();
        tracing::warn!(%status, body = %body, "Telegram API returned an error");
        return Err(AppError::Config(format!(
            "Telegram API returned non-success status: {}",
            status
        )));
    }
    Ok(())
}

fn format_telegram_message(message: &TelegramAlertMessage) -> String {
    let mut text = format!(
        "🚀 <b>Nouvelle tendance détectée</b>\n\n<b>{}</b>\nPlateforme: {}\n",
        html_escape(&message.title),
        html_escape(&message.platform)
    );
    if let Some(region) = &message.region {
        text.push_str(&format!("Région: {}\n", html_escape(region)));
    }
    if let Some(category) = &message.category {
        text.push_str(&format!("Catégorie: {}\n", html_escape(category)));
    }
    if let Some(vph) = message.views_per_hour {
        text.push_str(&format!("Vues / heure: {}\n", vph));
    }
    if let Some(score) = message.trend_score {
        text.push_str(&format!("Trend score: {:.1}\n", score));
    }
    if let Some(url) = &message.url {
        text.push_str(&format!(
            "\n<a href=\"{}\">Voir la tendance</a>",
            html_escape(url)
        ));
    }
    text
}

fn html_escape(input: &str) -> String {
    input
        .replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
}
