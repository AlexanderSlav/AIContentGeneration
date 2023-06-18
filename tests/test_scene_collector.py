from src.guess_by_frame.utils import Scene


mock_scene = Scene(path_to_image="path_to_image_1", movie_name="test_movie")
mock_scene_2 = Scene(path_to_image="path_to_image_2", movie_name="test_movie_2")

def test_scene_collector(scene_collector):
    # Test add_image and get_images
    scene_collector.add_scene(mock_scene)
    scene_collector.add_scene(mock_scene_2)
    assert scene_collector.get_scenes() == [mock_scene, mock_scene_2]
