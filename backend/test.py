try:
    from app.main import app
    print('App imported successfully')
except Exception as e:
    print(f'Import failed: {e}')
    import traceback
    traceback.print_exc()