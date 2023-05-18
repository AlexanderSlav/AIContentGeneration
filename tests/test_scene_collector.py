def test_scene_collector(scene_collector):
    # Test add_image and get_images
    scene_collector.add_image("path_to_image1")
    scene_collector.add_image("path_to_image2")
    assert scene_collector.get_images() == ["path_to_image1", "path_to_image2"]
