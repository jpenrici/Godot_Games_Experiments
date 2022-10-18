using Godot;
using System;

public class Ball : RigidBody
{
    private float speed;

    private Vector3 position;
    private Vector3 linearVelocity;

    public override void _Ready()
    {
        speed = 15f;
        position = Translation;

        Mass = 1f;
        Weight = 9.8f;
        CanSleep = false;
        PhysicsMaterialOverride.Rough = true;
        PhysicsMaterialOverride.Friction = 0.5f;
        PhysicsMaterialOverride.Bounce = 0.5f;
        LinearVelocity = new Vector3(0.0f, 0.0f, 0.0f);
        AngularVelocity = new Vector3(0.5f, 0.0f, 0.5f);

        linearVelocity = LinearVelocity;
    }

    public override void _Process(float delta)
    {
        if (Translation.y < -20)
        {
            Reposition();
        }
    }

    public void _on_Area_body_entered(Node body)
    {
        GD.Print(body.Name);
        if (body.Name.StartsWith("Foot", StringComparison.Ordinal))
        {
            LinearVelocity += new Vector3(speed * (LinearVelocity.x > 0 ? 1f : -1f), 0.0f, 0.0f);
        }
    }

    public void _on_Ball_mouse_entered()
    {
        Reposition();
    }

    private void Reposition()
    {
        Translation = position;
        LinearVelocity = linearVelocity;
    }
}
