using Godot;
using System;

public class Table : Spatial
{
    public void _on_Goal_A_body_entered(Node body)
    {
        if (body.Name.Equals("Ball"))
        {
            GD.Print("Team A :: Goal");
        }
    }

    public void _on_Goal_B_body_entered(Node body)
    {
        if (body.Name.Equals("Ball"))
        {
            GD.Print("Team A :: Goal");
        }
    }

}
