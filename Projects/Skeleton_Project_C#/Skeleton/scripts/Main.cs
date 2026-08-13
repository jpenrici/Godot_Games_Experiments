using Godot;
using System;

public class Main : Node2D
{
    private Node2D Skeleton;
    private Image ImageShot;
    private Sprite Photo;

    public override void _Ready()
    {
        Skeleton = GetNode<Node2D>("Skeleton");
        Skeleton.Position = new Vector2(195, 235);

        Photo = GetNode<Node2D>("ImageShot").GetNode<Sprite>("Photo");

        GD.Print(string.Format("{0} : main script ...", Name));
    }

    private void _on_Cam_button_down()
    {
        Image imageTemp = GetViewport().GetTexture().GetData();
        imageTemp.FlipY();

        ImageShot = imageTemp.GetRect(new Rect2(10, 50, 360, 350));
        if (ImageShot != null)
        {
            var tex = new ImageTexture();
            tex.CreateFromImage(ImageShot);
            Photo.Texture = tex;
        }
    }

    private void _on_Download_button_down()
    {
        if (ImageShot != null)
        {
            var now = DateTime.Now;
            var filename = string.Format("skeleton_{0}-{1}-{2}_{3}{4}{5}",
                now.Year, now.Month, now.Day, now.Hour, now.Minute, now.Second);
            ImageShot.SavePng(filename);
            GD.Print("Image saved:", filename);
        }
    }

    private void _on_Reset_button_down()
    {
        Skeleton.EmitSignal("Reset");
    }

}
