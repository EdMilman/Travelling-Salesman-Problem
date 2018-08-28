from cities import *
import pytest


@pytest.fixture(scope="module")
def road_map_big():
    road_map = read_cities("city-data.txt")
    return road_map


@pytest.fixture()
def road_map_small():
    road_map_s = read_cities("city-small.txt")
    return road_map_s


@pytest.fixture(scope="module")
def gps():
    d = {"montgomery": (32.361538, -86.279118), "juneau": (58.301935, -134.41974), "phoenix": (33.448457, -112.073844),
         "little_rock": (34.736009, -92.331122), "sacremento": (38.555605, -121.468926)}
    return d


# mont -> juneau + juneau -> phoenix + phoenix -> l rock + l rock -> sacramento + sacramento -> juneau
def test_compute_total_distance(road_map_small, gps):
    assert compute_total_distance(road_map_small) == (distance(*gps["montgomery"], *gps["juneau"]) +
                                                      distance(*gps["juneau"], *gps["phoenix"]) +
                                                      distance(*gps["phoenix"], *gps["little_rock"]) +
                                                      distance(*gps["little_rock"], *gps["sacremento"]) +
                                                      distance(*gps["sacremento"], *gps["montgomery"]))


def test_compute_total_distance_fail(road_map_small):
    assert compute_total_distance(road_map_small) != 42


# check swapping 0th item with 1th item
def test_swap_adjacent_cities(road_map_small, gps):
    assert swap_adjacent_cities(road_map_small, 0) == ([('Alaska', 'Juneau', 58.301935, -134.41974),
                                                        ('Alabama', 'Montgomery', 32.361538, -86.279118),
                                                        ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                        ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                        ('California', 'Sacramento', 38.555605, -121.468926)],
                                                       (distance(*gps["juneau"], *gps["montgomery"]) +
                                                        distance(*gps["montgomery"], *gps["phoenix"]) +
                                                        distance(*gps["phoenix"], *gps["little_rock"]) +
                                                        distance(*gps["little_rock"], *gps["sacremento"]) +
                                                        distance(*gps["sacremento"], *gps["juneau"])))


# check swapping last item with 0th item
def test_swap_adjacent_cities2(road_map_small, gps):
    assert swap_adjacent_cities(road_map_small, 4) == ([('California', 'Sacramento', 38.555605, -121.468926),
                                                        ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                        ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                        ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                        ('Alabama', 'Montgomery', 32.361538, -86.279118)],
                                                       (distance(*gps["sacremento"], *gps["juneau"]) +
                                                        distance(*gps["juneau"], *gps["phoenix"]) +
                                                        distance(*gps["phoenix"], *gps["little_rock"]) +
                                                        distance(*gps["little_rock"], *gps["montgomery"]) +
                                                        distance(*gps["montgomery"], *gps["sacremento"])))


def test_swap_adjacent_cities_fail(road_map_small, gps):
    assert swap_adjacent_cities(road_map_small, 4) != ([('Alabama', 'Montgomery', 32.361538, -86.279118),
                                                        ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                        ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                        ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                        ('California', 'Sacramento', 38.555605, -121.468926)],
                                                       (distance(*gps["montgomery"], *gps["little_rock"]) +
                                                        distance(*gps["little_rock"], *gps["phoenix"]) +
                                                        distance(*gps["phoenix"], *gps["juneau"]) +
                                                        distance(*gps["juneau"], *gps["sacremento"]) +
                                                        distance(*gps["sacremento"], *gps["montgomery"])))


def test_swap_cities_normal(road_map_small, gps):
    assert swap_cities(road_map_small, 1, 3) == ([('Alabama', 'Montgomery', 32.361538, -86.279118),
                                                  ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                  ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                  ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                  ('California', 'Sacramento', 38.555605, -121.468926)],
                                                 (distance(*gps["montgomery"], *gps["little_rock"]) +
                                                  distance(*gps["little_rock"], *gps["phoenix"]) +
                                                  distance(*gps["phoenix"], *gps["juneau"]) +
                                                  distance(*gps["juneau"], *gps["sacremento"]) +
                                                  distance(*gps["sacremento"], *gps["montgomery"])))


def test_swap_cities_normal_fail(road_map_small, gps):
    assert swap_cities(road_map_small, 1, 3) != ([('California', 'Sacramento', 38.555605, -121.468926),
                                                  ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                  ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                  ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                  ('Alabama', 'Montgomery', 32.361538, -86.279118)],
                                                 (distance(*gps["sacremento"], *gps["juneau"]) +
                                                  distance(*gps["juneau"], *gps["phoenix"]) +
                                                  distance(*gps["phoenix"], *gps["little_rock"]) +
                                                  distance(*gps["little_rock"], *gps["montgomery"]) +
                                                  distance(*gps["montgomery"], *gps["sacremento"])))


def test_swap_cities_same_index(road_map_small, gps):
    assert swap_cities(road_map_small, 2, 2) == ([('Alabama', 'Montgomery', 32.361538, -86.279118),
                                                  ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                  ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                  ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                  ('California', 'Sacramento', 38.555605, -121.468926)],
                                                 (distance(*gps["montgomery"], *gps["phoenix"]) +
                                                  distance(*gps["phoenix"], *gps["juneau"]) +
                                                  distance(*gps["juneau"], *gps["little_rock"]) +
                                                  distance(*gps["little_rock"], *gps["sacremento"]) +
                                                  distance(*gps["sacremento"], *gps["montgomery"])))


def test_swap_cities_same_index_fail(road_map_small, gps):
    assert swap_cities(road_map_small, 2, 2) != ([('California', 'Sacramento', 38.555605, -121.468926),
                                                  ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                  ('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                  ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                  ('Alabama', 'Montgomery', 32.361538, -86.279118)],
                                                 (distance(*gps["sacremento"], *gps["juneau"]) +
                                                  distance(*gps["juneau"], *gps["phoenix"]) +
                                                  distance(*gps["phoenix"], *gps["little_rock"]) +
                                                  distance(*gps["little_rock"], *gps["montgomery"]) +
                                                  distance(*gps["montgomery"], *gps["sacremento"])))


# in find_best_cycle set swaps = 8, random.seed(1)
@pytest.mark.xfail
def test_find_best_cycle(road_map_small):
    assert find_best_cycle(road_map_small) == ([('Arizona', 'Phoenix', 33.448457, -112.073844),
                                                ('Alabama', 'Montgomery', 32.361538, -86.279118),
                                                ('Arkansas', 'Little Rock', 34.736009, -92.331122),
                                                ('Alaska', 'Juneau', 58.301935, -134.41974),
                                                ('California', 'Sacramento', 38.555605, -121.468926)],
                                               6501.711059227743)
