// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![run_scan])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

#[tauri::command]
fn run_scan(url: String) -> String {
    use std::process::Command;

    let output = Command::new("python")
        .arg("python/run_scan.py")
        .arg(&url)
        .output()
        .expect("failed to execute Python script");

    String::from_utf8_lossy(&output.stdout).to_string()
}



