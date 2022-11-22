using Godot;

public class SpriteAction : Sprite
{
    [Export]
    public bool adjust_rotation = false;

    public override void _Ready()
    {
        GD.Print(string.Format("{0} : action script ...", Name));
    }

    public override void _Process(float delta)
    {
        if (Name.Equals(SkelectonControl.ObjSelected))
        {
            var rotation = GetLocalMousePosition().Angle() - Mathf.Deg2Rad(90);
            if (adjust_rotation)
            {
                rotation += Mathf.Deg2Rad(180);
            }
            Rotation += rotation;
        }
    }

    private void _on_Area2D_mouse_entered()
    {
        SkelectonControl.ObjMouse = Name;
        GD.Print(string.Format("{0} ...", Name));

        Modulate = new Color(0f, 0.9f, 0.7f, 1f);
    }

    private void _on_Area2D_mouse_exited()
    {
        Modulate = new Color(1f, 1f, 1f, 1f);
    }
}
