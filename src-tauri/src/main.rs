// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use serde_json::Value;

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![run_scan])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

#[tauri::command]
fn run_scan(url: String) -> Result<Value, String> {
    use std::process::Command;

    let output = Command::new("python")
        .current_dir("..")
        .arg("python/run_scan.py")
        .arg(&url)
        .output()
        .map_err(|e| e.to_string())?;

    serde_json::from_slice(&output.stdout).map_err(|e| e.to_string())
}



