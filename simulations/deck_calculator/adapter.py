from simulations.sphere_space_station_simulations import SphereDeckCalculator


def main():
    calculator = SphereDeckCalculator(
        "Deck Dimensions of a Sphere",
        sphere_diameter=127.0,
        hull_thickness=0.5,
        windows_per_deck_ratio=0.20,
        num_decks=16,
        deck_000_outer_radius=10.5,
        deck_height_brutto=3.5,
        deck_ceiling_thickness=0.5,
    )

    calculator.calculate_dynamics_of_a_sphere(angular_velocity=0.5)
    calculator.to_csv("deck_dimensions.csv")
    calculator.to_html("deck_dimensions.html")
    calculator.to_3D_animation_rotate_hull_with_gravity_zones(
        "hull_with_gravity_zones_animation.html",
        frames=25,
        frames_per_second=25,
        rotation_axis="Z",
        show_gravity_zones=False,
    )


if __name__ == "__main__":
    main()
