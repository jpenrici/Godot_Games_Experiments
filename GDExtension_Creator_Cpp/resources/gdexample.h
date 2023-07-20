#ifndef #GDEXTENSIONH#_H
#define #GDEXTENSIONH#_H

#include <godot_cpp/classes/sprite2d.hpp>

namespace godot {

class #GDEXTENSIONCLASS# : public Sprite2D {
    GDCLASS(#GDEXTENSIONCLASS#, Sprite2D)

private:
    int variable;

protected:
    static void _bind_methods();

public:
    #GDEXTENSIONCLASS#();
    ~#GDEXTENSIONCLASS#();

    void _ready();
    void _process(double delta);
};

}

#endif // #GDEXTENSIONH#_H