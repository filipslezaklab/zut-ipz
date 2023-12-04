use clap::Parser;
use serde::Serialize;

#[derive(Clone, Debug, Serialize, Parser)]
pub struct Config {
    #[arg(
        long,
        env = "DB_URL",
        default_value = "mongodb://ipz:ipz@127.0.0.1:27017/"
    )]
    pub db_url: String,
}

impl Config {
    #[must_use]
    pub fn new() -> Self {
        let mut config = Self::parse();
        config
    }
}
