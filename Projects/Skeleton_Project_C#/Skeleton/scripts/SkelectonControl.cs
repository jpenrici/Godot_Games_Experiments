using Godot;

public class SkelectonControl : Node2D
{
    private Sprite Head;
    private Sprite Body;
    private Sprite LeftArm1;
    private Sprite LeftArm2;
    private Sprite LeftHand;
    private Sprite LeftLeg1;
    private Sprite LeftLeg2;
    private Sprite LeftFoot;
    private Sprite RightArm1;
    private Sprite RightArm2;
    private Sprite RightHand;
    private Sprite RightLeg1;
    private Sprite RightLeg2;
    private Sprite RightFoot;

    public static string ObjSelected { get; set; } = "";
    public static string ObjMouse { get; set; } = "";

    [Signal]
    private delegate void Reset();

    public override void _Ready()
    {
        Head = GetNode<Sprite>("Head");
        Body = GetNode<Sprite>("Body");
        LeftArm1 = GetNode<Sprite>("LeftArm1");
        LeftArm2 = GetNode<Sprite>("LeftArm2");
        LeftHand = GetNode<Sprite>("LeftHand");
        LeftLeg1 = GetNode<Sprite>("LeftLeg1");
        LeftLeg2 = GetNode<Sprite>("LeftLeg2");
        LeftFoot = GetNode<Sprite>("LeftFoot");
        RightArm1 = GetNode<Sprite>("RightArm1");
        RightArm2 = GetNode<Sprite>("RightArm2");
        RightHand = GetNode<Sprite>("RightHand");
        RightLeg1 = GetNode<Sprite>("RightLeg1");
        RightLeg2 = GetNode<Sprite>("RightLeg2");
        RightFoot = GetNode<Sprite>("RightFoot");

        Body.Set("adjust_rotation", true);
        Head.Set("adjust_rotation", true);

        Body.Scale = new Vector2(0.45f, 0.45f);
        Head.Scale = Body.Scale;
        LeftArm1.Scale = Body.Scale;
        LeftArm2.Scale = Body.Scale;
        LeftHand.Scale = Body.Scale;
        LeftLeg1.Scale = Body.Scale;
        LeftLeg2.Scale = Body.Scale;
        LeftFoot.Scale = Body.Scale;
        RightArm1.Scale = Body.Scale;
        RightArm2.Scale = Body.Scale;
        RightHand.Scale = Body.Scale;
        RightLeg1.Scale = Body.Scale;
        RightLeg2.Scale = Body.Scale;
        RightFoot.Scale = Body.Scale;

        _on_Skeleton_Reset();

        GD.Print(string.Format("{0} : skeleton control ...", Name));
    }

    public override void _Process(float delta)
    {
        Connect();

        if (Input.IsActionJustPressed("select"))
        {
            GD.Print(string.Format("{0} selected ...", ObjSelected));
            ObjSelected = ObjMouse;
            ObjMouse = "";
        }
        if (Input.IsActionJustPressed("deselect"))
        {
            ObjMouse = "";
            ObjSelected = "";
            GD.Print("Released objects ...");
        }
    }

    private void Connect()
    {
        Head.Position = Body.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        LeftArm1.Position = Body.GetNode<Position2D>("Pos2D1").GlobalPosition - Position;
        LeftArm2.Position = LeftArm1.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        LeftHand.Position = LeftArm2.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        LeftLeg1.Position = Body.GetNode<Position2D>("Pos2D3").GlobalPosition - Position;
        LeftLeg2.Position = LeftLeg1.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        LeftFoot.Position = LeftLeg2.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        RightArm1.Position = Body.GetNode<Position2D>("Pos2D2").GlobalPosition - Position;
        RightArm2.Position = RightArm1.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        RightHand.Position = RightArm2.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        RightLeg1.Position = Body.GetNode<Position2D>("Pos2D4").GlobalPosition - Position;
        RightLeg2.Position = RightLeg1.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
        RightFoot.Position = RightLeg2.GetNode<Position2D>("Pos2D").GlobalPosition - Position;
    }

    public void _on_Skeleton_Reset()
    {
        Body.Rotation = 0f;
        Head.Rotation = Body.Rotation;
        LeftArm1.Rotation = Body.Rotation + Mathf.Deg2Rad(30);
        LeftArm2.Rotation = Body.Rotation;
        LeftHand.Rotation = Body.Rotation;
        LeftLeg1.Rotation = Body.Rotation + Mathf.Deg2Rad(15);
        LeftLeg2.Rotation = Body.Rotation;
        LeftFoot.Rotation = Body.Rotation;
        RightArm1.Rotation = Body.Rotation + Mathf.Deg2Rad(-30);
        RightArm2.Rotation = Body.Rotation;
        RightHand.Rotation = Body.Rotation;
        RightLeg1.Rotation = Body.Rotation + Mathf.Deg2Rad(-15);
        RightLeg2.Rotation = Body.Rotation;
        RightFoot.Rotation = Body.Rotation;
        GD.Print("Reset ...");
    }
}
