using Godot;

public class Player_A4 : Spatial
{
    float posX;
    float posY;

    public override void _Ready()
    {
        posX = Translation.x;
        posY = Translation.y;
    }

    public override void _Process(float delta)
    {
        PlayerControl.GetInput(this, new Vector3(posX, posY, Translation.z), true);
    }
}