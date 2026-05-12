import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

ApplicationWindow {
    id: root
    visible: true
    width: 400
    height: 750
    title: "CubAutosFinder"
    color: "#0d0d0d"

    property color gold: "#d4af37"
    property color orange: "#e85d04"
    property color card: "#1a1a1a"
    property color elevated: "#202020"
    property color text1: "#f5f5f5"
    property color text2: "#888888"

    property bool loading: apiClient.loading
    property int selectedIdx: -1

    Component.onCompleted: {
        apiClient.search("", 30, 0, 0, "", "")
    }

    StackView {
        id: nav
        anchors.fill: parent
        initialItem: homePage
    }

    // HOME PAGE
    Component {
        id: homePage

        Rectangle {
            color: "#0d0d0d"

            Column {
                anchors.fill: parent

                // Header
                Rectangle {
                    width: root.width
                    height: 60
                    color: "#1a1a1a"

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16

                        Column {
                            spacing: 2
                            anchors.verticalCenter: parent.verticalCenter

                            Text { text: "CubAutos"; font.pixelSize: 18; font.bold: true; color: gold }
                            Text { text: "Vehículos Eléctricos"; font.pixelSize: 10; color: text2 }
                        }

                        Item { width: root.width - 180 }

                        Rectangle {
                            width: 32
                            height: 32
                            radius: 16
                            border.color: gold
                            border.width: 2
                            visible: loading
                            anchors.verticalCenter: parent.verticalCenter

                            RotationAnimation on rotation {
                                from: 0; to: 360; duration: 1000; loops: Animation.Infinite
                            }
                        }

                        Text {
                            text: "✓"
                            font.pixelSize: 18
                            color: gold
                            visible: !loading
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                // Status
                Rectangle {
                    width: root.width
                    height: 30
                    color: "#161616"

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16

                        Text { text: apiClient.status; font.pixelSize: 11; color: loading ? gold : text2; anchors.verticalCenter: parent.verticalCenter }
                        Item { width: root.width - 200 }
                        Text { text: vehicleModel.count() + " resultados"; font.pixelSize: 11; color: gold; visible: vehicleModel.count() > 0; anchors.verticalCenter: parent.verticalCenter }
                    }
                }

                // Content
                Item {
                    width: root.width
                    height: root.height - 90

                    // Loading
                    Column {
                        anchors.centerIn: parent
                        visible: loading
                        spacing: 12

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            border.color: gold
                            border.width: 3

                            RotationAnimation on rotation {
                                from: 0; to: 360; duration: 1200; loops: Animation.Infinite
                            }
                        }

                        Text { text: "Cargando..."; font.pixelSize: 13; color: gold; anchors.horizontalCenter: parent.horizontalCenter }
                    }

                    // List
                    ListView {
                        id: lv
                        anchors.fill: parent
                        model: vehicleModel
                        visible: !loading
                        spacing: 10
                        clip: true
                        topMargin: 8
                        bottomMargin: 8
                        leftMargin: 12
                        rightMargin: 12

                        delegate: Item {
                            width: lv.width - 24
                            height: 145

                            Rectangle {
                                anchors.fill: parent
                                color: card
                                radius: 12

                                Row {
                                    anchors.fill: parent
                                    anchors.margins: 10
                                    spacing: 10

                                    Rectangle {
                                        width: 100
                                        height: parent.height
                                        color: elevated
                                        radius: 8
                                        clip: true

                                        Image {
                                            anchors.fill: parent
                                            anchors.margins: 3
                                            fillMode: Image.PreserveAspectCrop
                                            source: imageUrl || ""
                                        }

                                        Rectangle {
                                            x: 4; y: 4
                                            width: 50; height: 16
                                            color: elevated
                                            radius: 4

                                            Text { anchors.centerIn: parent; text: sourceLabel || source || ""; color: gold; font.pixelSize: 8; font.bold: true }
                                        }
                                    }

                                    Column {
                                        width: parent.width - 120
                                        height: parent.height
                                        spacing: 6

                                        Text { text: title || ""; font.pixelSize: 12; font.bold: true; color: text1; wrapMode: Text.WordWrap; maximumLineCount: 2 }
                                        Text { text: price > 0 ? "$" + price : "Consultar"; font.pixelSize: 16; font.bold: true; color: gold }
                                        Text { text: province || "Cuba"; font.pixelSize: 11; color: text2 }
                                        Text { text: autonomiaKm > 0 ? autonomiaKm + " km" : ""; font.pixelSize: 11; color: orange; visible: autonomiaKm > 0 }
                                        Item { width: 1; height: 1 }
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        selectedIdx = index
                                        nav.push(detailPage)
                                    }
                                }
                            }
                        }
                    }

                    // Empty
                    Column {
                        anchors.centerIn: parent
                        visible: !loading && vehicleModel.count() === 0
                        spacing: 10

                        Text { text: "🔍"; font.pixelSize: 36; anchors.horizontalCenter: parent.horizontalCenter }
                        Text { text: "Sin resultados"; font.pixelSize: 15; font.bold: true; color: text1 }
                    }
                }
            }
        }
    }

    // DETAIL PAGE - Fixed heights
    Component {
        id: detailPage

        Rectangle {
            color: "#0d0d0d"

            Column {
                anchors.fill: parent

                // Header
                Rectangle {
                    width: root.width
                    height: 54
                    color: "#1a1a1a"

                    Text {
                        text: "← Volver"
                        font.pixelSize: 14
                        color: gold
                        anchors.left: parent.left
                        anchors.leftMargin: 16
                        anchors.verticalCenter: parent.verticalCenter

                        MouseArea { anchors.fill: parent; onClicked: nav.pop() }
                    }

                    Text {
                        text: "Detalle"
                        font.pixelSize: 16
                        font.bold: true
                        color: text1
                        anchors.centerIn: parent
                    }
                }

                // Content with fixed sections
                Column {
                    width: root.width
                    height: root.height - 54

                    // Image - 180px
                    Rectangle {
                        width: root.width
                        height: 180
                        color: card

                        Image {
                            anchors.fill: parent
                            fillMode: Image.PreserveAspectCrop
                            source: vehicleModel.get(selectedIdx).imageUrl || ""
                        }

                        Rectangle {
                            anchors.top: parent.top
                            anchors.right: parent.right
                            anchors.margins: 10
                            width: 100
                            height: 28
                            color: gold
                            radius: 6

                            Text {
                                anchors.centerIn: parent
                                text: vehicleModel.get(selectedIdx).sourceLabel || ""
                                color: "#0d0d0d"
                                font.pixelSize: 11
                                font.bold: true
                            }
                        }
                    }

                    // Title - 85px
                    Rectangle {
                        width: root.width
                        height: 85
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 4

                            Text {
                                width: parent.width
                                text: vehicleModel.get(selectedIdx).title || ""
                                font.pixelSize: 15
                                font.bold: true
                                color: text1
                                wrapMode: Text.WordWrap
                                maximumLineCount: 2
                            }

                            Text {
                                text: vehicleModel.get(selectedIdx).price > 0 
                                    ? "$" + vehicleModel.get(selectedIdx).price + " " + (vehicleModel.get(selectedIdx).currency || "USD")
                                    : "Consultar precio"
                                font.pixelSize: 22
                                font.bold: true
                                color: gold
                            }

                            Text {
                                text: "📍 " + (vehicleModel.get(selectedIdx).province || "Cuba")
                                font.pixelSize: 11
                                color: text2
                            }
                        }
                    }

                    // Specs - 150px
                    Rectangle {
                        width: root.width
                        height: 150
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8

                            Text {
                                text: "Especificaciones"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Grid {
                                columns: 4
                                spacing: 6
                                width: parent.width

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "🔋"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Autonomía"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: {
                                                var v = vehicleModel.get(selectedIdx).autonomiaKm
                                                return v > 0 ? v + " km" : "N/A"
                                            }
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "⚡"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Batería"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: {
                                                var v = vehicleModel.get(selectedIdx).batteryKwh
                                                return v > 0 ? v + " kWh" : "N/A"
                                            }
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "⏱"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Carga"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: vehicleModel.get(selectedIdx).chargingTime || "N/A"
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "🚗"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Modelo"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: vehicleModel.get(selectedIdx).modelo || "N/A"
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Contact - 90px
                    Rectangle {
                        width: root.width
                        height: 90
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 6

                            Text {
                                text: "Contacto"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Text { text: "👤 " + (vehicleModel.get(selectedIdx).contactName || "No disponible"); font.pixelSize: 11; color: text1 }
                            Text { text: "📞 " + (vehicleModel.get(selectedIdx).contactPhone || "No disponible"); font.pixelSize: 11; color: text1 }
                            Text { text: "💬 " + (vehicleModel.get(selectedIdx).contactWhatsapp || "No disponible"); font.pixelSize: 11; color: orange }
                        }
                    }

                    // Description - 70px
                    Rectangle {
                        width: root.width
                        height: 70
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 4

                            Text {
                                text: "Descripción"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Text {
                                width: parent.width
                                text: vehicleModel.get(selectedIdx).description || "Sin descripción disponible."
                                font.pixelSize: 11
                                color: text2
                                wrapMode: Text.WordWrap
                                maximumLineCount: 3
                            }
                        }
                    }

                    // Button - 45px
                    Rectangle {
                        width: root.width
                        height: 45
                        color: gold
                        radius: 8

                        Text {
                            text: "Ver Anuncio Original"
                            color: "#0d0d0d"
                            font.bold: true
                            font.pixelSize: 14
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: Qt.openUrlExternally(vehicleModel.get(selectedIdx).url || "")
                        }
                    }
                }
            }
        }
    }
}