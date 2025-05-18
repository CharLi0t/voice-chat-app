mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = 8080\n\
enableCORS = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
