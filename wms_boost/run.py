import uvicorn


if __name__ == '__main__':
    uvicorn.run('app:app', port=5054, debug=True, access_log=False)
