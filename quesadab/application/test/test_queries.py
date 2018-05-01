def test_fixture(): #Need a new 'def test_*():' for every test you wish to run
    pytest.mark.usefixtures(getUsersTest())