import model ,sys
if __name__ == "__main__":
    place = f'>>'
    while True:
        sys._clear_type_cache()
        user_input = input(place)
        model_instance = model.Models(user_input)
        model_instance.process_input()