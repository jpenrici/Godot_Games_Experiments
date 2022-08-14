using Godot;

public class PlayerControl : Spatial
{
    private static bool isAttack = true;

    public static void GetInput(Spatial sp, Vector3 vec3, bool attack)
    {
        AnimationPlayer animationPlayer;
        animationPlayer = sp.GetNode<AnimationPlayer>("AnimationPlayer");

        isAttack &= !Input.IsActionPressed("defense");
        isAttack |= Input.IsActionPressed("attack");

        if (isAttack.Equals(attack))
        {
            if (Input.IsActionPressed("up"))
            {
                GD.Print(sp.Name, ": Up");
                sp.Translation = new Vector3(vec3.x, vec3.y, sp.Translation.z - 0.2f);
            }
            if (Input.IsActionPressed("down"))
            {
                GD.Print(sp.Name, ": Down");
                sp.Translation = new Vector3(vec3.x, vec3.y, sp.Translation.z + 0.2f);
            }
            if (Input.IsActionJustPressed("kick"))
            {
                if (!animationPlayer.Equals(null))
                {
                    if (!isAttack)
                    {
                        animationPlayer.Play("Action_A1");
                        animationPlayer.Play("Action_A2");
                        GD.Print("Defense");
                    }
                    else
                    {
                        animationPlayer.Play("Action_A3");
                        animationPlayer.Play("Action_A4");
                        GD.Print("Attack");
                    }
                }
            }
        }
    }
}
