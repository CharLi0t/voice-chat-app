mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = 8080\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml
