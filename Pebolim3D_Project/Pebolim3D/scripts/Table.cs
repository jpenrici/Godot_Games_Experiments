using Godot;
using System;

public class Table : Spatial
{
    private int score_team_A;
    private int score_team_B;
    Label Score_A;
    Label Score_B;

    public override void _Ready()
    {
        score_team_A = 0;
        score_team_B = 0;

        Score_A = GetNode<Label>("Score_A_Label");
        Score_B = GetNode<Label>("Score_B_Label");
    }

    public override void _Process(float delta)
    {
        Score_A.Text = string.Format("{0:00}", score_team_A);
        Score_B.Text = string.Format("{0:00}", score_team_B);
    }

    public void _on_Goal_A_body_entered(Node body)
    {
        if (body.Name.Equals("Ball"))
        {
            //GD.Print("Team B :: Goal");
            score_team_B++;
        }
    }

    public void _on_Goal_B_body_entered(Node body)
    {
        if (body.Name.Equals("Ball"))
        {
            //GD.Print("Team A :: Goal");
            score_team_A++;
        }
    }

}
