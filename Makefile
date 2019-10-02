target = 'data/movies/The.Exorcist.1973.Extended.Directors.Cut.BluRay.480p.H264.mp4'
#target = 'data/movies/Pretty.Woman.1990.Bluray.720p.H264.mp4'

all:
	echo "shot or join"


shot:
	python P1_shot_detection.py $(target)
	python P2_scene_change.py $(target)
	python P3_measure_scenes.py $(target)

join:
	python E0_extract_segments.py $(target)
	python E1_extract_audio.py $(target)
	python E2_combine.py $(target)
	python E3_detect_speech.py $(target)
	python E4_build_subset.py $(target)
