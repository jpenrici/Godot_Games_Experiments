using Godot;
using System;

public class Airplane : Spatial
{
    private Spatial airplane;
    private Spatial airplane_explode;
    private Vector3 scale_Min;
    private Vector3 scale_Max;
    private Vector3 scale_Step;
    private float speed;
    private float Y_Max;
    private float X_Max_CamTop;
    private float X_Max_CamBack;
    private float inclination;
    private static Vector3 coordinate;

    public override void _Ready()
    {
        speed = 10f;
        Y_Max = 10f;
        X_Max_CamTop = 15f;
        X_Max_CamBack = 8f;
        inclination = 20f;
        scale_Max = new Vector3(1f, 1f, 1f);
        scale_Min = new Vector3(0.1f, 0.1f, 0.1f);
        scale_Step = new Vector3(0.01f, 0.01f, 0.01f);

        airplane = GetNode<Spatial>("airplane");
        airplane.Visible = true;

        airplane_explode = GetNode<Spatial>("airplaneExplode");
        airplane_explode.Visible = false;
        airplane_explode.Scale = scale_Min;
    }

    public override void _Process(float delta)
    {
        Vector3 direction = Vector3.Zero;
        Vector3 rotation = Vector3.Zero;
        float X_Max = X_Max_CamBack;

        if (Main.IsCameraTop())
        {
            X_Max = X_Max_CamTop;
        }

        if (Input.IsActionPressed("up") && !Main.IsCameraTop())
        {
            direction.y = 1f * Convert.ToInt32(Translation.y < Y_Max);
        }
        if (Input.IsActionPressed("down") && !Main.IsCameraTop())
        {
            direction.y = -1f * Convert.ToInt32(Translation.y > 0);
        }
        if (Input.IsActionPressed("left"))
        {
            direction.x = -1f * Convert.ToInt32(Translation.x > -X_Max);
            rotation.z = inclination;
        }
        if (Input.IsActionPressed("right"))
        {
            direction.x = 1f * Convert.ToInt32(Translation.x < X_Max);
            rotation.z = -inclination;
        }

        if (!direction.Equals(Vector3.Zero))
        {
            Translation += direction * speed * delta;
        }

        if (airplane_explode.Visible)
        {
            airplane_explode.Scale += scale_Step;
            if (airplane_explode.Scale > scale_Max)
            {
                airplane_explode.Scale = scale_Min;
                airplane_explode.Visible = false;
                airplane.Visible = true;
            }
        }

        Rotation = rotation;
        coordinate = Translation;
    }

    public void _on_Area_area_entered(Area area)
    {
        if (area.Name.StartsWith("Obstacle", StringComparison.Ordinal))
        {
            //GD.Print(area.Name);
            airplane.Visible = false;
            airplane_explode.Visible = true;
        }
    }

    public static Vector3 Coordinate()
    {
        return coordinate;
    }
}
