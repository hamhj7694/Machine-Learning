from pathlib import Path
import runpy

app_file = Path(__file__).parent / "영화 추천 웹 대쉬보드" / "webapp.py"
runpy.run_path(str(app_file), run_name="__main__")
