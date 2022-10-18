using Godot;

public class Player : Spatial
{
    [Export]
    public readonly bool useArrow;

    [Export]
    public readonly float Z_Top;

    [Export]
    public readonly float Z_Bottom;

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
        if ((Input.IsActionPressed("up1") && !useArrow) || (Input.IsActionPressed("up2") && useArrow))
        {
            if (Translation.z > Z_Top)
            {
                Translation = new Vector3(position.x, position.y, Translation.z - step);
            }
        }
        if ((Input.IsActionPressed("down1") && !useArrow) || (Input.IsActionPressed("down2") && useArrow))
        {
            if (Translation.z < Z_Bottom)
            {
                Translation = new Vector3(position.x, position.y, Translation.z + step);
            }
        }
        if (action != null && ((Input.IsActionJustPressed("kick1") && !useArrow) || (Input.IsActionJustPressed("kick2") && useArrow)))
        {
            animationPlayer.Play(action);
        }
    }
}
