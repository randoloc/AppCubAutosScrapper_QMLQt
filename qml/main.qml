import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import QtQuick.Window 2.14
import QtQuick.Dialogs 1.3

ApplicationWindow {
    id: root
    visible: true
    width: 1200
    height: 800
    title: "CubAutosFinder"

    property bool isLoading: apiClient.loading
    property int selectedIndex: -1
    property string filterSources: ""
    property int filterMaxAds: 50
    property double filterMinPrice: 0
    property double filterMaxPrice: 0
    property string filterBrand: ""
    property string filterProvince: ""
    property bool srcRevolico: true
    property bool srcAtrexport: true
    property bool srcChinautoscuba: true
    property bool srcCubamotor: true

    property color primaryDark: "#1b4332"
    property color primaryMid: "#2d6a4f"
    property color primaryLight: "#40916c"
    property color primaryPale: "#52b788"
    property color primaryBg: "#d8f3dc"
    property color bgColor: "#f0f0f0"
    property color cardBg: "#ffffff"
    property color textColor: "#212529"
    property color textMuted: "#6c757d"
    property color borderColor: "#dee2e6"
    property color accentOrange: "#e76f51"

    header: Rectangle {
        height: 54
        color: primaryDark
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            Label {
                text: "CubAutosFinder"
                color: "white"
                font.pixelSize: 20
                font.bold: true
            }
            Item { Layout.fillWidth: true }
            Label {
                id: statusLbl
                text: apiClient.status
                color: "#cccccc"
                font.pixelSize: 13
            }
            BusyIndicator {
                running: isLoading
                width: 22; height: 22
            }
        }
    }

    SplitView {
        anchors.fill: parent
        orientation: Qt.Vertical

        Rectangle {
            SplitView.preferredHeight: 170
            color: cardBg
            border.color: borderColor
            border.width: 1

            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                clip: true

                GridLayout {
                    columns: 4
                    columnSpacing: 14
                    rowSpacing: 8

                    Label { text: "Precio min ($):"; font.pixelSize: 12; color: textMuted }
                    SpinBox {
                        id: minPriceSp
                        from: 0; to: 500000; stepSize: 500; value: 0
                        editable: true
                        Layout.fillWidth: true
                        onValueChanged: filterMinPrice = value
                    }

                    Label { text: "Precio max ($):"; font.pixelSize: 12; color: textMuted }
                    SpinBox {
                        id: maxPriceSp
                        from: 0; to: 500000; stepSize: 500; value: 0
                        editable: true
                        Layout.fillWidth: true
                        onValueChanged: filterMaxPrice = value
                    }

                    Label { text: "Marca:"; font.pixelSize: 12; color: textMuted }
                    ComboBox {
                        id: brandCombo
                        model: ["Todas", "BYD", "Tesla", "Nissan", "BMW"]
                        Layout.fillWidth: true
                        onCurrentTextChanged: filterBrand = currentText !== "Todas" ? currentText : ""
                    }

                    Label { text: "Provincia:"; font.pixelSize: 12; color: textMuted }
                    ComboBox {
                        id: provinceCombo
                        model: ["Todas", "La Habana", "Matanzas"]
                        Layout.fillWidth: true
                        onCurrentTextChanged: filterProvince = currentText !== "Todas" ? currentText : ""
                    }

                    Label { text: "Max resultados:"; font.pixelSize: 12; color: textMuted }
                    SpinBox {
                        id: maxAdsSp
                        from: 5; to: 200; stepSize: 5; value: 50
                        editable: true
                        Layout.fillWidth: true
                        onValueChanged: filterMaxAds = value
                    }

                    Item { Layout.fillWidth: true }

                    Label { text: "Fuentes:"; font.pixelSize: 12; color: textMuted }
                    RowLayout {
                        Layout.columnSpan: 2
                        spacing: 10
                        CheckBox { text: "Revolico"; checked: true }
                        CheckBox { text: "Atrexport"; checked: true }
                        CheckBox { text: "ChinautosCuba"; checked: true }
                        CheckBox { text: "CubaMotor"; checked: true }
                    }

                    Button {
                        Layout.columnSpan: 2
                        Layout.fillWidth: true
                        text: "Buscar"
                        enabled: !isLoading
                        font.bold: true
                        background: Rectangle {
                            color: !parent.enabled ? "#aaa" : parent.hovered ? primaryMid : primaryDark
                            radius: 4
                        }
                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font: parent.font
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        onClicked: {
                            vehicleModel.clear()
                            selectedIndex = -1
                            apiClient.search("", filterMaxAds, filterMinPrice, filterMaxPrice, filterBrand, filterProvince)
                        }
                    }
                }
            }
        }

        Rectangle {
            color: bgColor
            RowLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 8

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: cardBg
                    radius: 4
                    border.color: borderColor
                    border.width: 1

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 4
                        spacing: 4

                        Label {
                            id: countLbl
                            text: vehicleModel.count() > 0 ? vehicleModel.count() + " resultados" : "Sin resultados"
                            font.pixelSize: 12
                            color: textMuted
                        }

                        ScrollView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true

                            GridView {
                                id: gridView
                                cellWidth: 310
                                cellHeight: 280
                                model: vehicleModel
                                clip: true

                                delegate: Rectangle {
                                    width: 296
                                    height: 272
                                    color: gridView.currentIndex === index ? primaryBg : "#ffffff"
                                    border.color: gridView.currentIndex === index ? primaryLight : borderColor
                                    border.width: gridView.currentIndex === index ? 2 : 1
                                    radius: 6

                                    ColumnLayout {
                                        anchors.fill: parent
                                        anchors.margins: 8
                                        spacing: 4

                                        Rectangle {
                                            Layout.fillWidth: true
                                            height: 150
                                            color: "#e9ecef"
                                            radius: 4
                                            clip: true

                                            Image {
                                                anchors.fill: parent
                                                anchors.margins: 2
                                                fillMode: Image.PreserveAspectCrop
                                                source: imageUrl || ""
                                                asynchronous: true
                                                cache: true
                                            }

                                            Rectangle {
                                                anchors.top: parent.top
                                                anchors.left: parent.left
                                                anchors.margins: 4
                                                color: primaryDark
                                                radius: 3
                                                height: 18
                                                width: srcLbl.contentWidth + 10
                                                Text {
                                                    id: srcLbl
                                                    anchors.centerIn: parent
                                                    text: sourceLabel || source || ""
                                                    color: "white"
                                                    font.pixelSize: 9
                                                    font.bold: true
                                                }
                                            }

                                            Rectangle {
                                                anchors.bottom: parent.bottom
                                                anchors.right: parent.right
                                                anchors.margins: 4
                                                color: "black"
                                                radius: 3
                                                height: 22
                                                width: priceLbl.contentWidth + 14
                                                Text {
                                                    id: priceLbl
                                                    anchors.centerIn: parent
                                                    text: price > 0 ? "$" + price + " " + currency : "Consultar"
                                                    color: "white"
                                                    font.pixelSize: 12
                                                    font.bold: true
                                                }
                                            }
                                        }

                                        Text {
                                            text: title
                                            font.pixelSize: 12
                                            font.bold: true
                                            color: textColor
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                            maximumLineCount: 1
                                        }

                                        Row {
                                            spacing: 12
                                            Text {
                                                text: autonomiaKm > 0 ? "Bateria: " + autonomiaKm + " km" : ""
                                                font.pixelSize: 10
                                                color: textMuted
                                            }
                                            Text {
                                                text: modelo ? "Modelo: " + modelo : ""
                                                font.pixelSize: 10
                                                color: textMuted
                                            }
                                        }

                                        Text {
                                            text: province ? "Provincia: " + province : ""
                                            font.pixelSize: 10
                                            color: textMuted
                                        }
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            gridView.currentIndex = index
                                            selectedIndex = index
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.preferredWidth: 340
                    Layout.fillHeight: true
                    color: cardBg
                    radius: 4
                    border.color: borderColor
                    border.width: 1
                    visible: selectedIndex >= 0

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 6

                        Label {
                            text: selectedIndex >= 0 ? vehicleModel.get(selectedIndex).title : ""
                            font.pixelSize: 14
                            font.bold: true
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }

                        Label {
                            text: selectedIndex >= 0 && vehicleModel.get(selectedIndex).price > 0 ?
                                  "$" + vehicleModel.get(selectedIndex).price + " " + vehicleModel.get(selectedIndex).currency :
                                  "Consultar"
                            font.pixelSize: 18
                            font.bold: true
                            color: primaryMid
                        }

                        Button {
                            Layout.fillWidth: true
                            text: "Abrir anuncio original"
                            enabled: selectedIndex >= 0 && vehicleModel.get(selectedIndex).url.length > 0
                            onClicked: Qt.openUrlExternally(vehicleModel.get(selectedIndex).url)
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: apiClient
        onErrorOccurred: function(error) {
            console.log("Error:", error)
        }
    }
}
