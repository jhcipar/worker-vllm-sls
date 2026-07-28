from src.engine_manager import EngineManager


class TestEngineManager:
    def test_defers_engine_creation_until_requested(self):
        created = []

        def factory():
            created.append(True)
            return object(), object()

        engines = EngineManager(factory)

        assert created == []
        assert engines.get()[0] is engines.get()[0]
        assert created == [True]

    def test_uses_one_until_the_engine_is_available(self):
        class VLLMEngine:
            max_concurrency = 8

        engines = EngineManager(lambda: (VLLMEngine(), object()))

        assert engines.max_concurrency == 1
        engines.get()
        assert engines.max_concurrency == 8
