import be.bootstrap as bootstrap
import bases.app as applib

class TestDispatcher:

    def setup(self):
        bootstrap.start('conf_test')

        class Maths: pass
        maths = Maths()
        maths.add = lambda x,y: x+y

        mapper = applib.Mapper()
        mapper.connect_collection('maths', maths)
        locator = mapper.build()
        root = applib.Dispatcher(locator, env.pg_provider)
        self.root = root

    def test_call(self):
        assert self.root.maths.add(2, 3) == (0,5)

    def test_calls(self):
        assert [self.root.maths.add(2, 3)*5] == [(0,5)*5]
