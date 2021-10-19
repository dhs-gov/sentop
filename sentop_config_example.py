# To use this configuration file, rename as 'sentop_config.py'.


# PostgreSQL configuration
database = {
      "url": "127.0.0.1",
      "database": "mydatabase",
      "username": "username",
      "password": "password"
}

data_dir_path = {
      "input": "C:\\my\\http\\server\\input_directory",
      "output": "C:\\my\\output_directory"
}

# Results generation. Here, JSON results are provided in the HTTP query
# response.
results = {
      "database": True,
      "json": True,
      "excel": True
}