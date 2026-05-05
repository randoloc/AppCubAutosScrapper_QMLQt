QT += quick network

CONFIG += c++11

TARGET = CubAutosFinder

SOURCES += \
    src/main.cpp \
    src/vehiclemodel.cpp \
    src/apiclient.cpp

HEADERS += \
    src/vehiclemodel.h \
    src/apiclient.h

RESOURCES += \
    qml.qrc

INSTALLS += target
