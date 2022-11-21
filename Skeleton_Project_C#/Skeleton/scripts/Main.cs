using Godot;
using System;

public class Main : Node2D
{
    private Node2D Skeleton;

    public override void _Ready()
    {
        Skeleton = GetNode<Node2D>("Skeleton");
        GD.Print(string.Format("{0} : main script ...", Name));
    }

    private void _on_Cam_button_down()
    {
        var now = DateTime.Now;
        var filename = string.Format("skeleton_{0}-{1}-{2}_{3}{4}{5}",
            now.Year, now.Month, now.Day, now.Hour, now.Minute, now.Second);
        var img = GetViewport().GetTexture().GetData();
        img.FlipY();
        img.SavePng(filename);
        GD.Print(filename);
    }

    private void _on_Reset_button_down()
    {
        Skeleton.EmitSignal("Reset");
    }
}
