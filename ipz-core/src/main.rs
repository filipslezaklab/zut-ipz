use axum::{routing::get, Router};
use config::Config;
use log::info;
use mongodb::{
    bson::doc,
    options::{ClientOptions, ServerApi, ServerApiVersion},
    Client,
};
use std::error::Error;

mod config;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    if dotenvy::from_filename(".env.local").is_err() {
        dotenvy::dotenv().ok();
    }

    env_logger::init();

    let config = Config::new();

    let mut client_options = ClientOptions::parse(config.db_url).await?;
    let server_api = ServerApi::builder().version(ServerApiVersion::V1).build();
    client_options.server_api = Some(server_api);
    let client = Client::with_options(client_options)?;
    client
        .database("admin")
        .run_command(doc! { "ping": 1 }, None)
        .await?;
    info!("Database connected");

    let app = Router::new().route("/", get(|| async { "Hi, from axum !" }));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
    Ok(())
}
