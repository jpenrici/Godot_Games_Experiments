using Godot;

public class Obstacle : Spatial
{
    private float speed;
    private float speed_Min;
    private float speed_Max;
    private float Z_Max;
    private Vector3 coordinate;

    public override void _Ready()
    {
        Z_Max = 25f;
        coordinate = Translation;

        speed_Min = 10f;
        speed_Max = 35f;
        Reposition();
    }

    public override void _Process(float delta)
    {
        Translation += new Vector3(0f, 0f, 1f) * speed * delta;
        Rotation += new Vector3(0.1f, 0f, 0.1f);

        if (Translation.z > Z_Max)
        {
            Reposition();
        }
    }

    private void Reposition()
    {
        Vector3 vec = Airplane.Coordinate();
        Translation = new Vector3(vec.x, vec.y, coordinate.z);
        Rotation = Vector3.Zero;

        speed = (float)GD.RandRange(speed_Min, speed_Max);
        //GD.Print(string.Format("{0} : Coordinate {1} : Speed = {2}", Name, Translation, speed));
    }

}
