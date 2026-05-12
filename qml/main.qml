import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import QtQuick.Window 2.14
import QtGraphicalEffects 1.14

ApplicationWindow {
    id: root
    visible: true
    width: isMobile ? Screen.width : 420
    height: isMobile ? Screen.height : 750
    title: "CubAutosFinder"
    color: bgPrimary

    readonly property bool isMobile: Screen.width < 500

    property bool isLoading: apiClient.loading
    property int selectedIndex: -1
    property int filterMaxAds: 30
    property double filterMinPrice: 0
    property double filterMaxPrice: 0
    property string filterBrand: ""
    property bool filtersOpen: false

    // Colors - Elegant Dark & Gold/Orange
    property color bgPrimary: "#0d0d0d"
    property color bgSecondary: "#161616"
    property color bgCard: "#1a1a1a"
    property color bgElevated: "#202020"
    property color goldPrimary: "#d4af37"
    property color goldLight: "#f4cf57"
    property color orangeWarm: "#e85d04"
    property color textPrimary: "#f5f5f5"
    property color textSecondary: "#888888"
    property color borderSubtle: "#333333"
    property color borderActive: "#d4af37"

    // Auto-search on startup
    Component.onCompleted: {
        apiClient.search("", 30, 0, 0, "", "")
    }

    // Header
    Rectangle {
        height: 70
        width: parent.width
        color: "#1a1a1a"

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20

            ColumnLayout {
                spacing: 0
                Label {
                    text: "CubAutos"
                    font.pixelSize: 22
                    font.bold: true
                    color: goldPrimary
                }
                Label {
                    text: "Vehículos Eléctricos Cuba"
                    font.pixelSize: 11
                    color: textSecondary
                }
            }

            Item { Layout.fillWidth: true }

            // Loading indicator
            Rectangle {
                width: 36
                height: 36
                radius: 18
                color: "transparent"
                border.color: goldPrimary
                border.width: 3
                visible: isLoading
                RotationAnimation on rotation {
                    from: 0; to: 360; duration: 1000; loops: Animation.Infinite
                }
                Text {
                    text: "✓"
                    font.pixelSize: 20
                    color: goldPrimary
                    anchors.centerIn: parent
                    visible: !isLoading
                }
            }
        }
    }

    // Status bar
    Rectangle {
        width: parent.width
        height: 36
        color: bgSecondary
        RowLayout {
            anchors.fill: parent
            anchors.margins: 16

            Text {
                text: apiClient.status
                font.pixelSize: 12
                color: isLoading ? goldPrimary : textSecondary
            }

            Item { Layout.fillWidth: true }

            Text {
                text: vehicleModel.count() + " resultados"
                font.pixelSize: 12
                color: goldPrimary
                visible: vehicleModel.count() > 0
            }
        }
    }

    // Filters Section - Elegant
    Rectangle {
        width: parent.width
        height: filtersOpen ? 260 : 52
        color: bgSecondary
        clip: true

        Behavior on height {
            NumberAnimation { duration: 350; easing.type: Easing.InOutCubic }
        }

        ColumnLayout {
            anchors.fill: parent

            // Toggle
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 52
                color: "transparent"

                Rectangle {
                    width: parent.width
                    height: 1
                    color: borderSubtle
                    anchors.bottom: parent.bottom
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16

                    Label {
                        text: "Filtros"
                        font.pixelSize: 14
                        font.bold: true
                        color: goldPrimary
                    }

                    Item { Layout.fillWidth: true }

                    Text {
                        text: filtersOpen ? "▲" : "▼"
                        font.pixelSize: 12
                        color: textSecondary
                    }
                }
            }

            // Filters content
            ScrollView {
                visible: filtersOpen
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                ColumnLayout {
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: parent.width - 40
                    spacing: 16
//                    padding.top: 16

                    // Price range
                    RowLayout {
                        width: parent.width
                        spacing: 12
                        ColumnLayout {
                            Layout.fillWidth: true
                            Label { text: "Precio mínimo"; font.pixelSize: 11; color: textSecondary }
                            TextField {
                                width: parent.width
                                placeholderText: "0"
                                background: Rectangle { color: bgCard; radius: 6; border.width: 1; border.color: borderSubtle }
                                placeholderTextColor: textSecondary
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            Label { text: "Precio máximo"; font.pixelSize: 11; color: textSecondary }
                            TextField {
                                width: parent.width
                                placeholderText: "50000"
                                background: Rectangle { color: bgCard; radius: 6; border.width: 1; border.color: borderSubtle }
                                placeholderTextColor: textSecondary
                            }
                        }
                    }

                    // Brand
                    Label { text: "Marca"; font.pixelSize: 11; color: textSecondary }
                    ComboBox {
                        width: parent.width
                        model: ["Todas las marcas", "BYD", "Tesla", "Nissan", "BMW", "Chevrolet"]
                        background: Rectangle { color: bgCard; radius: 6; border.width: 1; border.color: borderSubtle }
                    }

                    // Search button
                    Button {
                        width: parent.width
                        height: 44
                        background: Rectangle {
                            color: goldPrimary
                            radius: 8
                        }
                        contentItem: Text {
                            text: "BUSCAR"
                            color: "#0d0d0d"
                            font.bold: true
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                        }
                        onClicked: {
                            vehicleModel.clear()
                            selectedIndex = -1
                            apiClient.search("", filterMaxAds, 0, 0, "", "")
                        }
                    }
                }
            }
        }
    }

    // Loading overlay
    Rectangle {
        visible: isLoading
        width: parent.width
        height: parent.height - 160
        y: 160
        color: "transparent"

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 16

            Rectangle {
                width: 50
                height: 50
                radius: 25
                color: "transparent"
                border.color: goldPrimary
                border.width: 3
                RotationAnimation on rotation {
                    from: 0; to: 360; duration: 1200; loops: Animation.Infinite
                }
            }

            Text {
                text: "Obteniendo datos..."
                font.pixelSize: 14
                color: goldPrimary
            }
        }
    }

    // Results List
    ListView {
        visible: !isLoading
        width: parent.width
        height: parent.height - 160
        y: 160
        model: vehicleModel
        spacing: 12

        delegate: Rectangle {
            width: parent.width - 24
            height: 160
            x: 12
            color: bgCard
            radius: 12
            border.width: 1
            border.color: selectedIndex === index ? goldPrimary : borderSubtle

            // Selected glow
            Rectangle {
                visible: selectedIndex === index
                anchors.fill: parent
                radius: 12
                color: "transparent"
                border.width: 2
                border.color: goldPrimary
                opacity: 0.4
            }

            RowLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 12

                // Image
                Rectangle {
                    Layout.preferredWidth: 110
                    Layout.fillHeight: true
                    radius: 8
                    color: bgElevated

                    Image {
                        anchors.fill: parent
                        anchors.margins: 4
                        fillMode: Image.PreserveAspectCrop
                        source: imageUrl || ""
                    }

                    // Source badge
                    Rectangle {
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.margins: 6
                        width: 50
                        height: 20
                        color: bgElevated
                        radius: 4
                        border.width: 1
                        border.color: borderSubtle
                        Text {
                            text: sourceLabel || source || ""
                            color: goldPrimary
                            font.pixelSize: 9
                            font.bold: true
                            anchors.centerIn: parent
                        }
                    }
                }

                // Info
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4

                    Text {
                        text: title || "Sin título"
                        font.pixelSize: 13
                        font.bold: true
                        color: textPrimary
                        wrapMode: Text.WordWrap
                        maximumLineCount: 2
                    }

                    Text {
                        text: price > 0 ? "$" + price + " " + (currency || "USD") : "Consultar precio"
                        font.pixelSize: 18
                        font.bold: true
                        color: goldPrimary
                    }

                    RowLayout {
                        spacing: 4
                        Text {
                            text: "📍"
                            font.pixelSize: 10
                            color: textSecondary
                        }
                        Text {
                            text: province || "Cuba"
                            color: textSecondary
                            font.pixelSize: 11
                        }
                    }

                    Text {
                        text: autonomiaKm > 0 ? "🔋 " + autonomiaKm + " km autonomía" : ""
                        color: orangeWarm
                        font.pixelSize: 11
                        visible: autonomiaKm > 0
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: selectedIndex = index
            }
        }
    }

    // Empty state
    Rectangle {
        visible: !isLoading && vehicleModel.count() === 0
        width: parent.width
        height: 200
        y: 200
        color: "transparent"

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 12

            Text {
                text: "🔍"
                font.pixelSize: 40
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                text: "Sin resultados"
                font.pixelSize: 16
                font.bold: true
                color: textPrimary
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                text: "Intenta con otros filtros"
                font.pixelSize: 13
                color: textSecondary
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
