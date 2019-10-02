target = 'data/movies/The.Exorcist.1973.Extended.Directors.Cut.BluRay.480p.H264.mp4'

all:
	python P1_shot_detection.py $(target)
	python P2_scene_change.py $(target)
	python P3_measure_scenes.py $(target)
	python E0_extract_segments.py $(target)
	python E1_extract_audio.py $(target)
	python E2_combine.py $(target)

	export GOOGLE_APPLICATION_CREDENTIALS="MovieTags-ce65c97a4c6b.json"
	python E2_combine.py $(target)
