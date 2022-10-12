using Godot;
using System;

public class Ball : Spatial
{
    float posX;
    float posY;
    RigidBody rb;

    public override void _Ready()
    {
        posX = Translation.x;
        posY = Translation.y;

        rb = this.GetNode<RigidBody>("RigidBody");
        rb.Mass = 0.01f;
        rb.Weight = 0.1f;
        rb.CanSleep = false;
        rb.PhysicsMaterialOverride.Rough = true;
        rb.PhysicsMaterialOverride.Friction = 0.1f;
        rb.PhysicsMaterialOverride.Bounce = 0.5f;
        rb.LinearVelocity = new Vector3(2.0f, 0.0f, 0.0f);
        rb.AngularVelocity = new Vector3(10.0f, 0.0f, 10.0f);
    }

    public override void _Process(float delta)
    {
    }

}
