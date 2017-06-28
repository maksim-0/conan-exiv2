#include <exiv2/exiv2.hpp>
#include <iostream>

int main(int argc, char **argv)
{
    if (argc != 2) {
        std::cerr << "Syntax: " << argv[0] << " inputImage" << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "Input file: " << argv[1] << std::endl;

    try {
        Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(argv[1]);
        image->readMetadata();
        auto data = image->exifData();

        for(auto it = data.begin(); it != data.end(); ++it)
        {
                // print the EXIF Key string
            std::cout << std::left << std::setw(40) << it->key().c_str() << "\t";

            // print the EXIF type string
            auto typeId = "[" + std::string(Exiv2::TypeInfo::typeName(it->typeId())) + "]";

            if(it->typeId() == Exiv2::undefined) {
                std::cout << typeId << "\n";
            } else if(it->value().count() > 10 && it->typeId() != Exiv2::asciiString) {
                std::cout << typeId << " x " << it->value().count() << " : {" << it->toString() << "}\n";
            } else {
                std::cout << std::setw(10) << typeId << "\t" << it->toString().c_str() << "\n";
            }
        }
    }
    catch(const Exiv2::AnyError& e)
    {
        std::cerr << "Exif error: " << e.what();
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
