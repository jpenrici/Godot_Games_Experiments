using Godot;

public class Main : Spatial
{
    private Camera camera1;
    private Camera camera2;
    private static bool isCameraTop;

    public override void _Ready()
    {
        camera1 = GetNode<Camera>("Camera_Top");
        camera1.Current = false;

        camera2 = GetNode<Camera>("Camera_Back");
        camera2.Current = true;
    }

    public override void _Process(float delta)
    {
        if (Input.IsActionJustPressed("space"))
        {
            if (camera1.Equals(GetViewport().GetCamera()))
            {
                camera1.Current = false;
                camera2.Current = true;
            }
            else
            {
                camera1.Current = true;
                camera2.Current = false;
            }
            isCameraTop = camera1.Current;
        }
    }

    public static bool IsCameraTop() => isCameraTop;
}
