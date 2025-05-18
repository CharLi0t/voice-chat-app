mkdir -p ~/.streamlit/

echo "\
[server]
headless = true
port = 8080
enableCORS = false
" > ~/.streamlit/config.toml
