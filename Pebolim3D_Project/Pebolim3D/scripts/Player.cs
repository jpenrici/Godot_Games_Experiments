using Godot;

public class Player : Spatial
{
    private Vector3 position;
    private AnimationPlayer animationPlayer;
    private string action;
    private readonly float step = 0.2f;

    public override void _Ready()
    {
        position = Translation;
        animationPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
        action = Name.Replace("Player", "Action");
    }

    public override void _Process(float delta)
    {
        if (Input.IsActionPressed("up"))
        {
            //GD.Print(Name, ": Up");
            Translation = new Vector3(position.x, position.y, Translation.z - step);
        }
        if (Input.IsActionPressed("down"))
        {
            //GD.Print(Name, ": Down");
            Translation = new Vector3(position.x, position.y, Translation.z + step);
        }
        if (action != null && Input.IsActionJustPressed("kick"))
        {
            animationPlayer.Play(action);
        }
    }
}
