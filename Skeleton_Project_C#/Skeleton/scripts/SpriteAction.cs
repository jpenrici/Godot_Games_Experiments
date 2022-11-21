using Godot;

public class SpriteAction : Sprite
{
    public override void _Ready()
    {
        GD.Print(string.Format("{0} : action script ...", Name));
    }

    public override void _Process(float delta)
    {
        if (Name.Equals(SkelectonControl.ObjSelected))
        {
            var rotation = GetLocalMousePosition().Angle();
            Rotation += rotation;
        }
    }

    private void _on_Area2D_mouse_entered()
    {
        SkelectonControl.ObjMouse = Name;
        GD.Print(string.Format("{0} ...", Name));
    }
}
