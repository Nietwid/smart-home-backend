from button.models import ButtonType, MonostableButtonEvent, BistableButtonEvent


def test_available_events_for_monostable(button):
    button.button_type = ButtonType.MONOSTABLE
    event = button.available_events()
    assert event == [event.value for event in MonostableButtonEvent]


def test_available_events_for_bistable(button):
    button.button_type = ButtonType.BISTABLE
    event = button.available_events()
    assert event == [event.value for event in BistableButtonEvent]


def test_available_events_for_invalid_type(button):
    button.button_type = "INVALID"
    event = button.available_events()
    assert event == []
